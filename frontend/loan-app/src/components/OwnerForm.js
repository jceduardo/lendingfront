import React from 'react'

const OwnerForm = ({ onChange, onSubmit, form }) => (
    <div className="container">
        <form onSubmit={onSubmit}>
            <div className="form-group">
                <input
                    type="number"
                    className="form-control"
                    name="owr_social_security_number"
                    onChange={onChange}
                    placeholder="Social Security Number"
                    value={form.own_social_security_number}
                    min="1"
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    name="owr_name"
                    onChange={onChange}
                    placeholder="Name"
                    value={form.owr_name}
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    name="owr_email"
                    onChange={onChange}
                    placeholder="Email"
                    value={form.owr_email}
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    name="owr_address"
                    onChange={onChange}
                    placeholder="Address"
                    value={form.owr_address}
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    name="owr_city"
                    onChange={onChange}
                    placeholder="City"
                    value={form.owr_city}
                />
            </div>
            <div className="form-group">
                <input
                    type="text"
                    className="form-control"
                    name="owr_state"
                    onChange={onChange}
                    placeholder="State"
                    value={form.owr_state}
                />
            </div>
            <div className="form-group">
                <input
                    type="number"
                    className="form-control"
                    name="owr_postal_code"
                    onChange={onChange}
                    placeholder="Postal Code"
                    value={form.owr_postal_code}
                />
            </div>
        </form>
    </div>
)

export default OwnerForm