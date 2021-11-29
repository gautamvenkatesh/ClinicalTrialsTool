/**
 * Display NavBar
 */
import React, { Component } from 'react'
import { Input, Menu } from 'semantic-ui-react'

import { NavLink } from 'react-router-dom'

export default class NavBar extends Component {
  render() {

    return (
      <Menu secondary>
        <Menu.Item
          as={NavLink} to="/"
          name='newtrials'
        />
        <Menu.Item
          as={NavLink} to="/search"
          name='search'
        />
      </Menu>

    );
  }
}
