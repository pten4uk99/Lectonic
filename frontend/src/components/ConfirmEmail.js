import React from "react";
import { useParams } from "react-router-dom";
import "../styles/ConfirmEmail.css";


export default function ConfirmEmail() {
    let params = useParams();
    console.log(params);
    return(
        <div>
            <h1>Url param is: { params.myId }</h1>
        </div>
    )
}