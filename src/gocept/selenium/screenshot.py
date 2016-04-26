from PIL import Image, ImageChops
import inspect
import itertools
import math
import os
import pkg_resources
import tempfile


SHOW_DIFF_IMG = os.environ.get('SHOW_DIFF_IMG', False)
PRINT_JUNIT_ATTACHMENTS = os.environ.get('GOCEPT_SELENIUM_JUNIT_ATTACH', False)


def get_path(resource):
    return pkg_resources.resource_filename('gocept.selenium', resource)


WHITE = (255, 255, 255, 0)


class DiffComposition(object):

    label_margin = 20

    def __init__(self, exp, got):
        self.exp = exp.convert('RGB')
        self.got = got.convert('RGB')
        self.width = self.exp.size[0]
        self.height = self.exp.size[1]
        self.prepare_composition()
        self.paste_screenshots()
        tmpfile, compo_path = tempfile.mkstemp(
            prefix='gocept_selenium_diff', suffix='.png')
        with open(compo_path, 'rw') as compo_file:
            self.path = compo_file.name
            self.compo.convert('RGB').save(self.path)
            if SHOW_DIFF_IMG:
                self.compo.show()
        os.close(tmpfile)

    def prepare_composition(self):
        """prepares and returns the composition image"""
        # NOTE: The method assumes that self.width/self.height is the
        # width/height of *all* of the images.

        # load the images with the labels
        exp_txt = Image.open(get_path('exp_txt.png'))
        got_txt = Image.open(get_path('got_txt.png'))
        diff_txt = Image.open(get_path('diff_txt.png'))
        # create emtpy image
        compo_size = (self.width, 3 * (self.height + self.label_margin))
        self.compo = Image.new('RGBA', compo_size, WHITE)
        # paste the labels onto it
        for index, img in enumerate((exp_txt, got_txt, diff_txt)):
            pos = (5, index * (self.height + self.label_margin))
            self.compo.paste(img, pos)

    def paste_screenshots(self):
        for index, screenshot in enumerate((self.exp, self.got, self.diff)):
            pos = (0, (index * self.height) +
                      ((index + 1) * self.label_margin))
            self.compo.paste(screenshot, pos)

    @property
    def diff(self):
        def subtract(source, sub):
            return ImageChops.invert(
                ImageChops.subtract(source, sub)).point(
                lambda i: 0 if i != 255 else 255).convert('1').convert(
                'RGB').split()[0]

        def paste(dest, bbox, channels, merged):
            mask = channels.point(lambda i: 80 if i != 255 else 255)
            dest.paste(merged, bbox, ImageChops.invert(mask))
        missing_red = subtract(self.got, self.exp)
        missing_green = subtract(self.exp, self.got)
        missing_empty = Image.new('L', missing_red.size, 255)
        missing_red_merged = Image.merge(
            'RGB',
            (missing_empty, missing_red, missing_red)).convert('RGBA')
        missing_green_merged = Image.merge(
            'RGB',
            (missing_green, missing_empty, missing_green)).convert('RGBA')
        diff = self.exp.copy()
        exp_bbox = diff.getbbox()
        mask = Image.new('L', (self.width, self.height), 127)
        diff.paste(self.got, exp_bbox, mask)
        paste(diff, exp_bbox, missing_red, missing_red_merged)
        paste(diff, exp_bbox, missing_green, missing_green_merged)
        return diff


class ImageDiff(object):

    def __init__(self, image_a, image_b):
        self.image_a = image_a
        self.image_b = image_b
        self.distance = self.get_nrmsd() * 100

    def within_threshold(self, threshold):
        return self.distance < threshold

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
            self.image_a.size[0] * self.image_a.size[1] * len(
                self.image_a.getbands())
        ))
        return rmsd / 255


def junit_attach_line(filename, typ):
    return '[[ATTACHMENT|%s|{"type": "%s"}]]\n' % (filename, typ)


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
        if PRINT_JUNIT_ATTACHMENTS:
            self._print_junit_attachments()

    def __str__(self):
        return self.message % (self.name, self.distance, self.expected,
                               self.got, self.compo)

    def _print_junit_attachments(self):
        print ('\n' +
               junit_attach_line(self.expected, 'expected') +
               junit_attach_line(self.got, 'actual') +
               junit_attach_line(self.compo, 'diff'))


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
        if PRINT_JUNIT_ATTACHMENTS:
            self._print_junit_attachments()

    def __str__(self):
        return self.message % (self.name, self.expected_size, self.got_size,
                               self.expected, self.got)

    def _print_junit_attachments(self):
        print ('\n' +
               junit_attach_line(self.expected, 'expected') +
               junit_attach_line(self.got, 'actual'))


class ZeroDimensionError(ValueError):

    def __init__(self, locator):
        self.locator = locator

    def __str__(self):
        return 'Either width or height of %r is zero.' % self.locator


def make_screenshot(selenese, locator):
    tmpfile, path = tempfile.mkstemp(
        prefix='gocept_selenium_screenshot')
    selenese.captureScreenshot(path)
    os.close(tmpfile)

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

    if 0 in (dimensions['width'], dimensions['height']):
        raise ZeroDimensionError(locator)

    with open(path, 'rw') as screenshot:
        box = (dimensions['left'], dimensions['top'],
               dimensions['left'] + dimensions['width'],
               dimensions['top'] + dimensions['height'])
        return Image.open(screenshot).convert('RGBA').crop(box)


def _screenshot_path(screenshot_directory):
    if screenshot_directory == '.':
        screenshot_directory = \
            inspect.currentframe().f_back.f_back.f_back.f_globals['__name__']
    return pkg_resources.resource_filename(screenshot_directory, '')


def save_screenshot_temporary(screenshot):
    """Saves given screenshot to a temporary file and return
    the filename."""
    tmpfile, got_path = tempfile.mkstemp(
        prefix='gocept_selenium_screenshot', suffix='.png')
    with open(got_path, 'rw') as got:
        screenshot.save(got.name)
    os.close(tmpfile)
    os.chmod(got_path, 0o644)
    return got.name


def save_as_expected(screenshot, img_basename, exp_path):
    if os.path.exists(exp_path):
        raise ValueError(
            'Not capturing {0}, image already exists. If you '
            'want to capture this element again, delete {1}'.format(
                img_basename, exp_path))
    screenshot.save(exp_path)
    raise ValueError(
        'Captured {0}. You might now want to remove capture mode and '
        'check in the created screenshot {1}.'.format(
            img_basename, exp_path))


def assertScreenshot(selenese, img_basename, locator, threshold=1):
    exp_path = os.path.join(
        _screenshot_path(selenese.screenshot_directory),
        '%s.png' % img_basename)
    screenshot = make_screenshot(selenese, locator)
    if selenese.capture_screenshot:
        # In capture mode, we only want to save the screenshot
        # as the new expected image.
        save_as_expected(screenshot, img_basename, exp_path)
        return
    exp = Image.open(exp_path)
    diff = ImageDiff(screenshot, exp)
    if not diff.within_threshold(threshold):
        # In failure case, we save the screenshot.
        got_path = save_screenshot_temporary(screenshot)
        if exp.size != screenshot.size:
            # Seperate exception if sizes differ.
            raise ScreenshotSizeMismatchError(
                img_basename, exp.size, screenshot.size, exp_path, got_path)
        # Sizes are the same, so we can render a nice diff image.
        compo = DiffComposition(exp, screenshot)
        raise ScreenshotMismatchError(
            img_basename, diff.distance, exp_path, got_path, compo.path)


def screenshot_window(selense):
    """Screenshot the whole browser window.

    Stores the result in a temporary file and returns the path to it.

    """
    return save_screenshot_temporary(make_screenshot(selense, 'css=body'))
