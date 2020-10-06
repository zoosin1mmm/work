import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { Router, Route, Link, browserHistory, IndexRoute  } from 'react-router'

ReactDOM.render((
   <Router history = {browserHistory}>
      <Route path = "/" component = {App}>
         <IndexRoute component = {Login} />
         <Route path = "" component = {Login} />
         // <Route path = "contact" component = {Contact} />
      </Route>
   </Router>
), document.getElementById('root'));
registerServiceWorker();
