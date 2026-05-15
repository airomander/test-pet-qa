Feature: User Login

  Scenario: Login with valid credentials
    Given I am on the login page
    When I login with "standard_user" and "secret_sauce"
    Then I should be on the inventory page

  Scenario: Login with invalid credentials
    Given I am on the login page
    When I login with "wrong_user" and "wrong_pass"
    Then I should see error "Username and password do not match"
