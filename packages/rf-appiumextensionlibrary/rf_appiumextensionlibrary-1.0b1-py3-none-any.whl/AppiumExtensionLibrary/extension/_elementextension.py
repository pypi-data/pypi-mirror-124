# Copyright (C) 2019 Shiela Buitizon | Joshua Kim Rivera

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from AppiumLibrary import (
        _WaitingKeywords,
        _ElementKeywords
    )
from robot.api import logger


class _ElementExtension(
    _WaitingKeywords,
    _ElementKeywords
):

    def clear_element_text(self, locator):
        """Clears the text field identified by `locator`.

           See `introduction` for details about locating elements.

           New in AppiumExtensionLibrary 0.9

           *AppiumExtensionLibrary Only Keyword*.
        """
        self.clear_text(locator)

    def get_element_count(self, locator):
        """ Returns the number of elements matching ``locator``.

            If you wish to assert the number of matching elements, use
            `Page Should Contain Element` with ``limit`` argument. Keyword will
            always return an integer.

            Example:
            | ${count} =       | `Get Element Count` | name:div_name  |
            | `Should Be True` | ${count} > 2        |                |

            *AppiumExtensionLibrary Only Keyword*.
        """
        return len(self._element_find(locator, False, False))

    def scroll_element_into_view(self, locator):
        """ Scrolls the element identified by ``locator`` into view.

            See the `Locating elements` section for details about the locator
            syntax.

            Web Context Only.

            New in AppiumExtensionLibrary 0.7

            *AppiumExtensionLibrary Only Keyword*.
        """
        element = self._element_find(locator, True, True)
        self._info("Scrolling Element {element} Into View".format(element=element,))
        self._current_application().execute_script("arguments[0].scrollIntoView();",
                                                   element)

    def set_focus_to_element(self, locator):
        """ Sets the focus to the element identified by ``locator``.

            Web Context Only.

            New in AppiumExtensionLibrary 0.7

            *AppiumExtensionLibrary Only Keyword*.
        """
        element = self._element_find(locator, True, True)
        self._current_application().execute_script("arguments[0].focus();", element)

    def element_shoud_not_be_visible(self, locator: str, loglevel='INFO'):
        """Verifies that the element identified by ``locator`` is NOT visible.

            New In AppiumExtensionLibrary 1.0

            *AppiumExtensionLibrary Only Keyword*.

            Passes if the element does not exists. See `Element Should Be Visible`
            for more information about visibility and supported arguments.
        """
        if not self._is_visible(locator):
            self.log_source(loglevel)
            logger.info(f'Element {locator} should not be visible but it is')
            raise AssertionError(f'Element {locator} should not be visible but it is.')

    def wait_until_element_is_not_visible(self, locator: str, timeout='3s'):
        """Waits until the element ``locator`` is visible.

            Fails if ``timeout`` expires before the element is visible. See
            the `Timeouts` section for more information about using timeouts and
            their default value and the `Locating elements` section for details
            about the locator syntax.

            New In AppiumExtensionLibrary 1.0

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._wait_until(
            timeout, f"Element '{locator}' still visible after {timeout}.",
            lambda: not self._is_visible(locator)
        )

    def wait_until_element_is_enabled(self, locator: str, timeout='3s'):
        """Waits until the element ``locator`` is enabled.

            Element is considered enabled if it is not disabled nor read-only.

            Fails if ``timeout`` expires before the element is enabled. See
            the `Timeouts` section for more information about using timeouts and
            their default value and the `Locating elements` section for details
            about the locator syntax.

            ``error`` can be used to override the default error message.

            Considering read-only elements to be disabled is a new feature
            in SeleniumLibrary 3.0.

            *AppiumExtensionLibrary Only Keyword*.
        """
        self._wait_until(
            timeout,  "Element '%s' was not enabled in <TIMEOUT>." % locator,
            lambda: self._element_find(locator, True, True).is_enabled()
        )
