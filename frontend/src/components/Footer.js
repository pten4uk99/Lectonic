import React from "react";
import { Link } from "react-router-dom";
import "../styles/Footer.css";
import instagram from "../img/footer-instagram.svg";
import vk from "../img/footer-vkontakte.svg";
import fb from "../img/footer-facebook.svg";

export default function Footer(){

    return(
        <footer>
            <div className="footer-wrapper">
                <div className="footer__rulesLinks">
                    <Link to=""><p className="footer__rulesLinks-text conditions">Условия использования</p></Link>
                    <Link to=""><p className="footer__rulesLinks-text">Политика конфиденциальности</p></Link>
                </div>

                <div className="footer__supportInfo">
                    <p className="footer__supportInfo-text">Техническая поддержка:<br/><span>support@lectonic.ru</span></p>
                </div>

                <div className="footer__socials">
                    <p className="footer__socials-text">Мы в соц. сетях:</p>
                    <div className="footer__socials-icons">
                        <a href="https://www.instagram.com/" target="_blank"><img src={instagram} alt="Instagram" /></a>
                        <a href="https://www.vk.com" target="_blank"><img src={vk} alt="VKontakte" /></a>
                        <a href="https://www.facebook.com" target="_blank"><img src={fb} alt="Facebook" /></a>
                    </div>
                </div>
            </div>
            <div className="footer__copyright">2022 © Сервис Lectonic</div>
        </footer>
    )
};
