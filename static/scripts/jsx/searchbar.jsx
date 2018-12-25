"use strict";

class Searchbar extends React.Component {
  render() {
    return (
        <div><p>Search Users</p>
        <form>
        <input
          type="text"
          placeholder="Search..."
          value={this.props.filterText}
          ref="filterTextInput"
          onChange={this.handleChange}
        />
        <p>
          <input
            type="checkbox"
            checked={this.props.inStockOnly}
            ref="inStockOnlyInput"
            onChange={this.handleChange}
          />
          {' '}
          Only show users in your area
        </p>
      </form>
        </div>
    );
  }
}


