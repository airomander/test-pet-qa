Feature: Inventory

  Scenario: View product list
    Given I am logged in as standard_user
    Then I should see 6 products in inventory

  Scenario: Add item to cart from inventory
    Given I am logged in as standard_user
    When I add "Sauce Labs Backpack" to cart
    Then the cart badge should show 1
