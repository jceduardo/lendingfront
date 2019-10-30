import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import LoanApp from '../pages/LoanApp'
import NotFound from '../pages/NotFound'

const LoanRouter = () => (
    <BrowserRouter>
        <Switch>
            <Route exact path="/loan_app" component={LoanApp} />
            <Route component={NotFound} />
        </Switch>
    </BrowserRouter>
)

export default LoanRouter