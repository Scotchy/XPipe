import React from 'react';
import ReactDOM from 'react-dom';
import { HeaderMenu } from './components/HeaderMenu';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { Link, BrowserRouter, Route } from "react-router-dom";
import { Index, Explorer, ExperimentPage } from "./pages";
import "bootstrap/dist/js/bootstrap";

ReactDOM.render(
	<React.StrictMode>
		<BrowserRouter>
			<HeaderMenu />
			<Route exact path="/" component={Index} />
			<Route path="/explorer" component={Explorer} />
			<Route path="/experiment" component={ExperimentPage} />
		</BrowserRouter>
		
	</React.StrictMode>,
	document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
