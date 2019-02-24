import React from 'react';
import PropTypes from 'prop-types';

import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import InputLabel from '@material-ui/core/InputLabel/InputLabel';
import Select from '@material-ui/core/Select/Select';
import MenuItem from '@material-ui/core/MenuItem/MenuItem';

import * as ScheduleEditorActions from '../../../../../redux/Actions/ScheduleEditorActions';
import { changeRouteSteps } from '../../../../../model/Redux/Page/ScheduleEditor';

class SelectRouteCodeAfterChangeRoute extends React.Component {
  constructor(props) {
    super(props);
    this.confirm = this.confirm.bind(this);
    this.back = this.back.bind(this);
    this.setSelectRouteCode = this.setSelectRouteCode.bind(this);
  }

  confirm() {
    if (this.props.routeCodeAfterChangeRoute.routeCode) {
      this.props.scheduleEditorActions.setChangeRouteActiveStepNext();
    } else {
      alert('Route Code is not selected!');
    }
  }

  back() {
    this.props.scheduleEditorActions.cancelSelectChangeRoute();
  }

  setSelectRouteCode(event) {
    const [
      routeCodeAfterChangeRoute
    ] = this.props.selectableChangeRouteList.filter(
      routeCode => routeCode.routeCode === event.target.value
    );

    if (routeCodeAfterChangeRoute) {
      this.props.scheduleEditorActions.setRouteCodeAfterChangeRoute(
        routeCodeAfterChangeRoute
      );
    } else {
      this.props.scheduleEditorActions.setRouteCodeAfterChangeRoute(null);
    }
  }

  getSelectItem() {
    const resList = [];

    resList.push(
      <MenuItem value="">
        <em>None</em>
      </MenuItem>
    );

    for (const routeCode of this.props.selectableChangeRouteList) {
      resList.push(
        <MenuItem value={routeCode.routeCode}>
          <em>{routeCode.routeCode}</em>
        </MenuItem>
      );
    }
    return resList;
  }

  render() {
    return (
      <Card shadow={0} style={{ width: '100%', minHeight: '100px' }}>
        <CardHeader
          title={changeRouteSteps[this.props.changeRouteActiveStep].name}
        />
        <CardContent>
          <InputLabel htmlFor="route-code">Route Code</InputLabel>
          <Select
            value={this.props.routeCodeAfterChangeRoute.routeCode}
            onChange={this.setSelectRouteCode}
            inputProps={{
              name: 'route-code'
            }}
            style={{ marginLeft: '5px' }}
          >
            {this.getSelectItem()}
          </Select>
        </CardContent>
        <CardActions>
          <div style={{ marginLeft: 'auto' }}>
            <Button onClick={this.back}>Back</Button>
            <Button
              color="primary"
              onClick={this.confirm}
              style={{ marginLeft: '5px' }}
            >
              Confirm
            </Button>
          </div>
        </CardActions>
      </Card>
    );
  }
}

SelectRouteCodeAfterChangeRoute.propTypes = {
  changeRouteActiveStep: PropTypes.string,
  routeCodeAfterChangeRoute: PropTypes.object,
  selectableChangeRouteList: PropTypes.array,
  scheduleEditorActions: PropTypes.object
};

const mapState = state => ({
  changeRouteActiveStep: state.scheduleEditor.getChangeRouteActiveStep(),
  routeCodeAfterChangeRoute: state.scheduleEditor.getRouteCodeAfterChangeRoute(),
  selectableChangeRouteList: state.scheduleEditor.getSelectableChangeRouteList()
});
const mapDispatch = dispatch => ({
  scheduleEditorActions: bindActionCreators(ScheduleEditorActions, dispatch)
});
export default connect(
  mapState,
  mapDispatch
)(SelectRouteCodeAfterChangeRoute);