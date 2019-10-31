import React from 'react'

const LoanResponseForm = ({ loanDecision, loanStatus }) => (
    <div className="container">
            <div className="form-group">
                <label>Loan Decision</label>
                <p>{loanDecision}</p>
            </div>
            <div className="form-group">
                <label>Loan Status</label>
                <p>{loanStatus}</p>
            </div>
    </div >
)

export default LoanResponseForm