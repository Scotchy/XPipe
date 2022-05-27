import React from 'react';
import ReactDOM from 'react-dom';
import { HeaderMenu } from './components/HeaderMenu';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { Link, BrowserRouter, Route, Switch } from "react-router-dom";
import { Index, Explorer, ExperimentPage } from "./pages";
import "bootstrap/dist/js/bootstrap";
import { CompareExperiments } from './pages/CompareExperimentsPage';
import { ENV, PROTOCOL, DEV_PORT } from './config';

export const appendScript = (src: string) => {
    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    document.body.appendChild(script);
}

// Import Bokeh js scripts
if (ENV == "dev") {
	// Import from the flask server
	appendScript(`${PROTOCOL}://localhost:${DEV_PORT}/bokeh.min.js`);
	appendScript(`${PROTOCOL}://localhost:${DEV_PORT}/bokeh-widgets.min.js`);
	appendScript(`${PROTOCOL}://localhost:${DEV_PORT}/bokeh-tables.min.js`);
	appendScript(`${PROTOCOL}://localhost:${DEV_PORT}/bokeh-api.min.js`);	
}
else {
	appendScript(`/bokeh.min.js`);
	appendScript(`/bokeh-widgets.min.js`);
	appendScript(`/bokeh-tables.min.js`);
	appendScript(`/bokeh-api.min.js`);
}

ReactDOM.render(
	<React.StrictMode>
		<BrowserRouter>
			<HeaderMenu />
			<Route exact path="/" component={Index} />
			<Route path="/explorer" component={Explorer} />
			<Route exact path="/compare" component={CompareExperiments} />
			<Switch>
				<Route path="/experiment/:exp_id" component={ExperimentPage} />
			</Switch>
		</BrowserRouter>
	</React.StrictMode>,
	document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
