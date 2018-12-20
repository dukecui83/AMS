import React from 'react';
import PropTypes from 'prop-types';

import { connect } from 'react-redux';

import { routeCodeSelector } from '../../../../../redux/selectors/ScheduleEditorSelector';

class RouteCodeUpdater extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    const routeCode = this.props.routeCode;
    console.log(routeCode);
    if (
      routeCode.startPoint !== null &&
      routeCode.laneList !== null &&
      routeCode.endPoint !== null
    ) {
      this.props.initRouteCode(routeCode);
    }
  }

  componentDidUpdate() {
    const routeCode = this.props.routeCode;
    if (
      routeCode.startPoint != null &&
      routeCode.laneList != null &&
      routeCode.endPoint != null
    ) {
      this.props.updateRouteCode(
        routeCode.startPoint,
        routeCode.laneList,
        routeCode.endPoint
      );
    }
  }

  render() {
    return <div />;
  }
}
RouteCodeUpdater.propTypes = {
  routeCode: PropTypes.object,
  initRouteCode: PropTypes.func,
  updateRouteCode: PropTypes.func
};

const mapState = state => ({
  routeCode: routeCodeSelector(state)
});
const mapDispatch = () => ({});
export default connect(
  mapState,
  mapDispatch
)(RouteCodeUpdater);