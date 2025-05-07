describe('Creating, toggling and removing to-do items from a task.', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let taskid // task id
  
    before(function () {
        // create a fabricated user from a fixture
        cy.fixture('user.json')
        .then((user) => {
          return cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
          });
        })
        .then((response) => {
          uid = response.body._id.$oid

          // Now load and process the task fixture after user is created
          return cy.fixture('task.json');
        })
        .then((task) => {
          task.userid = uid;
          
          // Extract todos array for special handling
          const todos = task.todos;
          delete task.todos;
          
          // Create formData object manually
          const formData = new FormData();
          Object.keys(task).forEach(key => {
            formData.append(key, task[key]);
          });
          
          // Add todos individually with the correct format 'todos'
          todos.forEach(todo => {
            formData.append('todos', todo);
          });
          
          // Send as raw form data instead of JSON
          return cy.request({
            method: 'POST',
            url: 'http://localhost:5000/tasks/create',
            body: formData,
            headers: {
              'Content-Type': 'multipart/form-data'
            },
            form: false
          });
        })
    });

    beforeEach(() => {
        cy.login("mon.doe@gmail.com");
        cy.contains('div', 'test').click();
    })

    it('creating a new to-do item', () => {
        cy.get('ul[class="todo-list"]')
        .find("input[type='text']")
        .type('Test to-do item')

        cy.get('ul[class="todo-list"]')
        .find("input[type='submit']")
        .click()

        cy.get('ul[class="todo-list"]')
        .should('contain.text', 'Test to-do item')
    })

    it('creating a new to-do item with no description', () => {
        cy.get('ul[class="todo-list"]')
        .find("input[type='submit']")
        .should('be.disabled')
    })

    it('toggle a to-do item unckecked', () => {
        cy.contains('li', 'Test to-do item').should('be.visible')
          .find('span[class="checker unchecked"]')
          .click()

        cy.contains('li', 'Test to-do item').should('be.visible')
          .find('span[class="checker checked"]')
          .should('have.class', 'checker checked')
    })

    it('toggle a to-do item ckecked', () => {
        cy.contains('li', 'Test to-do item').should('be.visible')
          .find('span[class="checker checked"]')
          .click()

        cy.contains('li', 'Test to-do item').should('be.visible')
          .find('span[class="checker unchecked"]')
          .should('have.class', 'checker unchecked')
    })

    it('deleting a to-do item', () => {
        cy.contains('li', 'Test to-do item').should('be.visible')
          .find('span[class="remover"]')
          .click()

        cy.get('ul[class="todo-list"]')
          .should('not.contain.text', 'Test to-do item')
    })

    after(function () {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })
    })
})