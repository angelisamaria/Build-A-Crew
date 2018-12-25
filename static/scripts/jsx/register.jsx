"use strict";

handleChange(event) {
  this.setState({email: event.target.value}
  this.setState({pw: event.target.value}
  this.setState({fname: event.target.value}
  this.setState({lname: event.target.value}
  this.setState({location: event.target.value}
  this.setState({portfolio: event.target.value})
}

class Register extends React.Component {
  render() {
    return (
        <div><p>Please Register</p>
        <form action="/register" method="post">
            Email: <input type="text" name="email" value={this.state.email} onChange={this.handleChange.bind(this)} />
            Password: <input type="password" name="pw" value={this.state.pw} onChange={this.handleChange.bind(this)} />
            First Name: <input type="text" name="fname" value={this.state.fname} onChange={this.handleChange.bind(this)} />
            Last Name: <input type="text" name="lname" value={this.state.lname} onChange={this.handleChange.bind(this)} />
            Location: <input type="text" name="location" value={this.state.location} onChange={this.handleChange.bind(this)} />
            Portfolio: <input type="url" name="portfolio" value={this.state.portfolio} onChange={this.handleChange.bind(this)} />
            <input type="submit"/>
        </form>
        <p>Already have an account?</p>
        <form method="GET" action="/login">
        <button type="submit">Login</button>
        </form>
        </div>
    );
  }
}

console.log(this.state.fname);