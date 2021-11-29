/**
 * Display NavBar
 */
import React, { Component } from 'react'
import { Input, Menu } from 'semantic-ui-react'

import { NavLink } from 'react-router-dom'

export default class NavBar extends Component {
  state = { activeItem: 'newtrials' }

  handleItemClick = (e : {}) => {
    this.setState({ activeItem: '' })
  }

  render() {
    const { activeItem } = this.state

    return (
      <Menu secondary>
        <Menu.Item
          as={NavLink} to="/"
          name='newtrials'
          active={activeItem === 'newtrials'}
          onClick={this.handleItemClick}
        />
        <Menu.Item
          as={NavLink} to="/search"
          name='search'
          active={activeItem === 'search'}
          onClick={this.handleItemClick}
        />
      </Menu>

    );
  }
}
