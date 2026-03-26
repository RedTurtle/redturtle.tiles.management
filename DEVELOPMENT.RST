======================
HOW TO DEVELOP PATTERN
======================


The pattern is located here: /resources/pat-tiles-management

Run "npx yarn install" to get the dependencies.
Run "npx yarn start" to start the development server for developing your pattern.
Run "npx yarn watch" to re-build the pattern into the Plone environment on changes.
Run "npx yarn run build" to compile the javascript bundle for production.

Note: You need to build the bundle before you can use the pattern in Plone.

Note: You might want to edit and fix the following file - there might be multiple
      "management-pattern-demo" view configurations in it:

./src/redturtle/tiles/management/browser/configure.zcml

There is a demo view for your pattern at:

http://localhost:8080/Plone/@@management-pattern-demo
