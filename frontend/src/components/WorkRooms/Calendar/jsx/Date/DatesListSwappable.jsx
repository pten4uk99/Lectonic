import React, {useEffect, useState} from "react";

import {connect} from "react-redux";
import DatesList from "./DatesList";
import {DeactivateSwap, DeactivateSwapClass} from "../../redux/actions/calendar";


function DatesListSwappable(props) {
    let [swapClass, setSwapClass] = useState("dates-list__wrapper");

    useEffect(() => {
        setSwapClass("dates-list__wrapper " + props.store.swapSideClass)
        setTimeout(() => {props.DeactivateSwapClass()}, 150)
    }, [props.store.swapSideClass])

    return (
            <div className={swapClass}>
                <DatesList/>
                <DatesList/>
                <DatesList/>
            </div>
    )
}

export default connect(
    state => ({store: state.calendar}),
    dispatch => ({
        DeactivateSwap:
            () => dispatch(DeactivateSwap()),
        DeactivateSwapClass:
            () => dispatch(DeactivateSwapClass())
    })
)(DatesListSwappable);
