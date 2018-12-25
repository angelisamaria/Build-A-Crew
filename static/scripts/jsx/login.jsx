"use strict";

class Login extends React.Component {
  render() {
    return (
        <div><p>Please Log In</p>
        <form action="/login" method="POST">
            Email: <input type="text" name="email"/>
            Password: <input type="password" name="pw"/>
            <input type="submit"/>
        </form>
        <p>Don't have an account?</p>
        <form method="GET" action="/register">
        <button type="submit">Register</button>
        </form>
        </div>
    );
  }
}