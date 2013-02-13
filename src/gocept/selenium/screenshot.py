from PIL import Image, ImageChops
import pkg_resources
import os
import tempfile
import math
import inspect
import itertools


SHOW_DIFF_IMG = os.environ.get('SHOW_DIFF_IMG', False)


def get_path(resource):
    return pkg_resources.resource_filename('gocept.selenium', resource)


def image_diff_composition(exp, got):
    exp = exp.convert('RGB')
    got = got.convert('RGB')
    exp_txt = Image.open(get_path('exp_txt.png'))
    got_txt = Image.open(get_path('got_txt.png'))
    diff_txt = Image.open(get_path('diff_txt.png'))
    mask = Image.new('L', exp.size, 127)
    compo = Image.new('RGBA', (exp.size[0], exp.size[1]*3+60), (255,255,255,0))
    compo.paste(exp_txt, (5,0))
    compo.paste(exp, (0,20))
    got_pos = (0, exp.size[1]+40)
    got_txt_pos = (5, exp.size[1]+20)
    diff_pos = (0, exp.size[1]*2+60)
    diff_txt_pos = (5, exp.size[1]*2+40)
    compo.paste(got_txt, got_txt_pos)
    compo.paste(got, got_pos)
    compo.paste(diff_txt, diff_txt_pos)
    missing_red = ImageChops.invert(
        ImageChops.subtract(got, exp)).point(
            lambda i: 0 if i!=255 else 255).convert('1').convert(
                'RGB').split()[0]
    missing_red_mask = missing_red.point(lambda i: 80 if i!=255 else 255)
    missing_empty = Image.new('L', missing_red.size, 255)
    missing_r = Image.merge(
        'RGB', (missing_empty, missing_red, missing_red)).convert('RGBA')
    missing_green = ImageChops.invert(
        ImageChops.subtract(exp, got)).point(
            lambda i: 0 if i!=255 else 255).convert('1').convert(
                'RGB').split()[0]
    missing_green_mask = missing_green.point(lambda i: 80 if i!=255 else 255)
    missing_g = Image.merge(
        'RGB', (missing_green, missing_empty, missing_green)).convert('RGBA')

    exp.paste(got, exp.getbbox(), mask)
    exp.paste(missing_r, exp.getbbox(), ImageChops.invert(missing_red_mask))
    exp.paste(missing_g, exp.getbbox(), ImageChops.invert(missing_green_mask))
    compo.paste(exp, diff_pos)
    return compo


class ImageDiff(object):

    def __init__(self, image_a, image_b):
        self.image_a = image_a
        self.image_b = image_b

    def get_nrmsd(self):
        """
        Returns the normalised root mean squared deviation of the two images.
        """
        a_values = itertools.chain(*self.image_a.getdata())
        b_values = itertools.chain(*self.image_b.getdata())
        rmsd = 0
        for a, b in itertools.izip(a_values, b_values):
            rmsd += (a - b) ** 2
        rmsd = math.sqrt(float(rmsd) / (
            self.image_a.size[0] * self.image_a.size[1] * len(self.image_a.getbands())
        ))
        return rmsd / 255


class ScreenshotMismatchError(ValueError):

    message = ("The saved screenshot for '%s' did not match the screenshot "
               "captured (by a distance of %.2f).\n\n"
               "Expected: %s\n"
               "Got: %s\n"
               "Diff: %s\n")

    def __init__(self, name, distance, expected, got, compo):
        self.name = name
        self.distance = distance
        self.expected = expected
        self.got = got
        self.compo = compo

    def __str__(self):
        return self.message % (self.name, self.distance, self.expected,
                               self.got, self.compo)


class ScreenshotSizeMismatchError(ValueError):

    message = ("Size of saved image for '%s', %s did not match the size "
               "of the captured screenshot: %s.\n\n"
               "Expected: %s\n"
               "Got: %s\n")

    def __init__(self, name, expected_size, got_size, expected, got):
        self.name = name
        self.expected_size = expected_size
        self.got_size = got_size
        self.expected = expected
        self.got = got

    def __str__(self):
        return self.message % (self.name, self.expected_size, self.got_size,
                               self.expected, self.got)


def _get_screenshot(selenese, locator):
    ignored, path = tempfile.mkstemp()
    selenese.captureScreenshot(path)

    dimensions = selenese.selenium.execute_script("""
        var e = arguments[0];
        var dimensions = {
            'width': e.offsetWidth,
            'height': e.offsetHeight,
            'left': 0,
            'top': 0
        };
        do {
            dimensions['left'] += e.offsetLeft;
            dimensions['top'] += e.offsetTop;
        } while (e = e.offsetParent)
        return dimensions;
        """, selenese._find(locator))

    with open(path, 'rw') as screenshot:
        box = (dimensions['left'], dimensions['top'],
               dimensions['left'] + dimensions['width'],
               dimensions['top'] + dimensions['height'])
        return Image.open(screenshot).convert('RGBA').crop(box)


def _screenshot_path(screenshot_directory):
    if screenshot_directory == '.':
        return os.path.dirname(inspect.getmodule(
            inspect.currentframe().f_back).__file__)
    return pkg_resources.resource_filename(
            screenshot_directory, '')


def assertScreenshot(selenese, name, locator, threshold=1):
    filename = os.path.join(
        _screenshot_path(selenese.screenshot_directory), '%s.png' % name)
    screenshot = _get_screenshot(selenese, locator)
    if selenese.capture_screenshot:
        if os.path.exists(filename):
            raise ValueError(
                'Not capturing {}, image already exists. If you '
                'want to capture this element again, delete {}'.format(
                    name, filename))
        screenshot.save(filename)
        raise ValueError(
            'Captured {}. You might now want to remove capture mode and '
            'check in the created screenshot {}.'.format(name, filename))
        return
    image = Image.open(filename)
    diff = ImageDiff(screenshot, image)
    distance = abs(diff.get_nrmsd()) * 100
    if distance > threshold:
        ignored, got_path = tempfile.mkstemp('.png')
        with open(got_path, 'rw') as got:
            screenshot.save(got.name)
        if image.size != screenshot.size:
            raise ScreenshotSizeMismatchError(
                name, image.size, screenshot.size, filename, got.name)
            return
        ignored, compo_path = tempfile.mkstemp('.png')
        with open(compo_path, 'rw') as compo:
            compo_img = image_diff_composition(image, screenshot)
            compo_img.save(compo.name)
            if SHOW_DIFF_IMG:
                compo_img.show()
        raise ScreenshotMismatchError(
            name, distance, filename, got.name, compo.name)

