var JSX = require('node-jsx').install(),
  React = require('react');

module.exports = {

  show: function(req, res) {
      // Render our 'home' template
      res.render('main.handlebars');
  },
  select: function(req, res) {
      // Render our 'home' template
      res.render('home.handlebars');
  }

}
