describe('Todo icon tests', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
    let title // task title to click

    before( () => {
      cy.fixture('user.json')
      .then( (user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
          cy.visit('http://localhost:3000')
          cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(email)
          cy.get('form').submit();
          cy.fixture('task.json')
          .then((task) => {
              title = task.title;
              cy.get('#title').type(task.title);
              cy.get('#url').type(task.url);
              cy.get('form').submit();
              cy.contains(title).click()
          });
        })
      })
    })

    beforeEach(() => {
      cy.visit('http://localhost:3000')
      cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
      cy.get('form').submit();
      cy.contains(title).click()
    })

    /*R8UC2 Case 1 */
    it('Testing to click todo - should be marked as done.', () => {
      cy.get('ul.todo-list li.todo-item span.checker').should('have.class', 'unchecked').click()
      cy.get('ul.todo-list li.todo-item span.checker').should('have.class', 'checked')
    });

    /*R8UC2 Case 2 */
    it('Testing to click todo - should be marked as not done.', () => {
      cy.get('ul.todo-list li.todo-item span.checker').should('have.class', 'checked').click()
      cy.get('ul.todo-list li.todo-item span.checker').should('have.class', 'unchecked')
    });

    after( () => {
        // clean up by deleting the user from the database
        cy.request({
                method: 'DELETE',
                url: `http://localhost:5000/users/${uid}`
              }).then((response) => {
                cy.log(response.body);
            });
        });
  })