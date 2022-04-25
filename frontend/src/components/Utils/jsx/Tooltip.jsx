import React, {useEffect, useState} from "react";


function Tooltip({width, posL, posT, posR, posB, corner, position, isVisible, text}){

    /*
    По props
    posY, posX - это координаты для положения подсказки на странице
    corner - это угол где будет отображаться стрелка (left-top - слева сверху, left-down слева снизу, right-top.. и тд)
    position - 'side' или 'outside' это где будет отображаться стрелка сбоку или сверху/снизу
    isVisible - это отображение, видно/не видно
    text - это текст
    */

    let [tooltip, setTooltip] = useState('tooltip ');
    let tooltipArrow = 'tooltip-arrow ';
    let arrow;
    let left = 0;
    let top = 0;
    
    
    useEffect(() => {
      if(isVisible) {
        setTooltip('tooltip tooltip-visible ')
      } else setTooltip('tooltip display-none ')
    }, [isVisible])

    switch (corner) {
        case 'left-top':
            tooltip += 'tooltip-top-left';
            if (position === 'side') {
                tooltipArrow += 'tooltip-arrow-up-left-side';
                arrow = 'arrow-up-side';
                left = -10;
                top = -1;
            } else if (position === 'outside'){
                tooltipArrow += 'tooltip-arrow-up-left-outside';
                arrow = 'arrow-left-outside';
                left = -1;
                top = -10;
            }
            break;
        case 'right-top':
            tooltip += 'tooltip-top-right';
            if (position === 'side') {
                tooltipArrow += 'tooltip-arrow-up-right-side';
                arrow = 'arrow-up-side';
                left = width - 2;
                top = -1;
            } else if (position === 'outside'){
                tooltipArrow += 'tooltip-arrow-up-right-outside';
                arrow = 'arrow-right-outside';
                left = width - 12;
                top = -10;
            }
            break;
        case 'left-down':
            tooltip += 'tooltip-down-left';
            if (position === 'side') {
                tooltipArrow += 'tooltip-arrow-down-left-side';
                arrow = 'arrow-down-side';
                left = -10;
                top = height - 11;
            } else if (position === 'outside'){
                tooltipArrow += 'tooltip-arrow-down-left-outside';
                arrow = 'arrow-left-outside';
                left = -1;
                top = height - 2;
            }
            break;
        case 'right-down':
            tooltip += 'tooltip-down-right';
            if (position === 'side') {
                tooltipArrow += 'tooltip-arrow-down-right-side';
                arrow = 'arrow-down-side';
                left = width - 2;
                top = height - 11;
            } else if (position === 'outside'){
                tooltipArrow += 'tooltip-arrow-down-right-outside';
                arrow = 'arrow-right-outside';
                left = width -12;
                top = height - 2;
            }
            break;
        default:
            break;
    }

    return (
        <div className={tooltip} style={{width: width || '',left: posL, top: posT, right: posR, bottom: posB}}>
            <div className={tooltipArrow} style={{left: left, top: top}}>
                <div className={arrow}/>
            </div>
            <p className="tooltip-text">{text}</p>
        </div>
    )
        
}

export default Tooltip;
