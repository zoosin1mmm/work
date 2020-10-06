import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

// class View extends Component {
//    constructor(props) {
//     super(props);
//   }
//   render() {
//     return (
//       <App><content><Login /></content></App>
//     );
//   }
// }
// export default View;

class App extends Component {
   constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          {this.props.content}
        </p>
      </div>
    );
  }
}

export default App;

class Login extends Component {
   constructor(props) {
    super(props);
    this.state = {password: '',account:''};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  handleChange(event) {
    this.setState({password: event.target.password});
  }
  handleSubmit(event) {
    if(this.state.password=='123'&&this.state.account=='123'){
      // this.result='登入成功'
    }
    else{
      this.result='登入失敗'
      event.preventDefault();
    }
  }
  render() {
    return (
      <form onSubmit={this.handleSubmit} action="/Content">
        <input type="text" value={this.state.account} onChange={this.handleChange} />
        <input type="password" value={this.state.password} onChange={this.handleChange} />
        <input type="submit" value="login" />
         {this.result}
      </form>
    );
  }
}

export default Login;