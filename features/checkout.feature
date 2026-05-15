Feature: Checkout Flow

  Scenario: Successful full purchase
    Given I am logged in as standard_user
    When I add "Sauce Labs Backpack" to cart
    And I add "Sauce Labs Bike Light" to cart
    And I proceed to checkout
    And I fill shipping details with "Roman" "Savchenko" "400001"
    And I finish the order
    Then I should see "Thank you for your order!"

  Scenario: Cancel at shipping form
    Given I am logged in as standard_user
    When I add "Sauce Labs Backpack" to cart
    And I proceed to checkout
    And I cancel checkout at step one
    Then I should be on cart page with 1 item

  Scenario: Required fields validation
    Given I am logged in as standard_user
    When I add "Sauce Labs Backpack" to cart
    And I proceed to checkout
    And I click continue without filling details
    Then I should see error "First Name is required"
