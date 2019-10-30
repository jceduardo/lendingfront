import React from 'react'

const BusinessForm = ({ onChange, onSubmit, form }) => (
    <div className="container">
        <form  onSubmit={onSubmit}>
            <div className="form-group">
                <input
                    type="number"
                    className="form-control"
                    name="bsn_tax_id"
                    onChange={onChange}
                    placeholder="Tax Id"
                    defaultValue={form.bsn_tax_id}
                    min="1"
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    name="bsn_name"
                    onChange={onChange}
                    placeholder="Business Name"
                    defaultValue={form.bsn_name}
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    name="bsn_address"
                    onChange={onChange}
                    placeholder="Business Address"
                    defaultValue={form.bsn_address}
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    name="bsn_city"
                    onChange={onChange}
                    placeholder="City"
                    defaultValue={form.bsn_city}
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    name="bsn_state"
                    onChange={onChange}
                    placeholder="State"
                    defaultValue={form.bsn_state}
                />
            </div>
            <div className="form-group">
                <input
                    type="number"
                    className="form-control"
                    name="bsn_postal_code"
                    onChange={onChange}
                    placeholder="Postal Code"
                    defaultValue={form.bsn_postal_code}
                />
            </div>
            <div className="form-group">
                <input
                    type="number"
                    className="form-control"
                    name="bsn_requested_amount"
                    onChange={onChange}
                    placeholder="Loan Request"
                    defaultValue={form.bsn_requested_amount}
                />
            </div>
        </form>
    </div >
)

export default BusinessForm