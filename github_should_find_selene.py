from selene import browser, be, have


browser.open('https://github.com/search')
browser.element('[aria-label="Search GitHub"]').type('qa.guru').press_enter()
browser.element('[data-testid="results-list"]').should(have.text('QA.GURU'))
