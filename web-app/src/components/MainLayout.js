import React, { Component } from 'react'
import { Button, Header, Icon, Menu, Sidebar, Grid } from 'semantic-ui-react'
import 'semantic-ui-less/semantic.less';


export default class MainHeader extends Component {
  state = { visible: false }

  handleShowClick = () => this.setState({ visible: true })
  handleSidebarHide = () => this.setState({ visible: false })

  render() {
    const { visible } = this.state

    return (

        <Grid columns = {16} celled centered> 
          <Grid.Column floated='left' width={1}>
            <Button icon disabled={visible} onClick={this.handleShowClick}>
              <Icon clolr = 'black' name = "align justify"/>
            </Button>

            <Sidebar
              as={Menu}
              animation='overlay'
              icon='labeled'
              inverted
              onHide={this.handleSidebarHide}
              vertical
              visible={visible}
              width='wide'
            >

              <Menu.Item as='a'>
                 물건 전달하기 
              </Menu.Item>
            </Sidebar>
          </Grid.Column>

          <Grid.Column width = {11} >
            <Grid centered>
              <Grid.Row>
                <Header size = 'huge'> Narumi</Header>
              </Grid.Row>
            </Grid>
          </Grid.Column>

          <Grid.Column floated='right' width = {4}>
            <Header size = 'large'>TASK LIST</Header>
          </Grid.Column>
        </Grid>
    )
  }
}