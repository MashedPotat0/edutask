describe('Todo create tests', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
    let title // task title to click

    beforeEach( () => {
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

    /*R8UC1 Case 3 */
    it('Testing to add a todo.', () => {
      cy.get('li').find('form')
      .find('input[type=text]')
      .type('This is just a test')
      cy.get('li').find('form')
      .find('input[type=submit]').click()

      cy.get('ul.todo-list').contains('This is just a test');
    });

    /*R8UC1 Case 2 */
    it('Add should be active when input is not empty.', () => {
      cy.get('li').find('form')
      .find('input[type=text]')
      .type('This is just a test')
      cy.get('li').find('form')
      .find('input[type=submit]')
      .should('be.enabled')
    });

    /*R8UC1 Case 1 */
    it('Add should be inactive when input is empty.', () => {
      cy.get('li').find('form')
      .find('input[type=submit]')
      .should('not.be.enabled')
    });

    afterEach( () => {
        // clean up by deleting the user from the database
        cy.request({
                method: 'DELETE',
                url: `http://localhost:5000/users/${uid}`
              }).then((response) => {
                cy.log(response.body);
            });
        });
  })