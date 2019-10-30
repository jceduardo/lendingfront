import React from 'react'
import ControlledTabs from '../components/ControlledTabs'

const LoanForm = ({ onChange, onSubmit, form }) => (
    <div className="card">
        <h5 className="card-header h5">Loan Application</h5>
        <div className="card-body">
            <div>
                <ControlledTabs
                    onChange={onChange}
                    onSubmit={onSubmit}
                    form={form}
                />
            </div>
            <div className="row justify-content-center">
                <div className="col-2">
                    <div className="card mb-1">
                        <button className="btn btn-success" onClick={onSubmit} type="button">
                            Send Loan Request
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
)


export default LoanForm
