import React, { useState } from 'react'
import 'bootstrap/dist/css/bootstrap.css'
import Tab from 'react-bootstrap/Tab'
import Tabs from 'react-bootstrap/Tabs'
import BusinessForm from './BusinessForm'
import OwnerForm from './OwnerForm'

function ControlledTabs({ onChange, onSubmit, form }) {
    const [key, setKey] = useState('business')

    return (
        <Tabs defaultActiveKey="profile" activeKey={key} onSelect={k => setKey(k)}>
            <Tab eventKey="business" title="Business">
                <BusinessForm 
                    onChange={onChange}
                    onSubmit={onSubmit}
                    form={form} 
                />
            </Tab>
            <Tab eventKey="owner" title="Owner">
                <OwnerForm 
                    onChange={onChange} 
                    onSubmit={onSubmit}
                    form={form} 
                />
            </Tab>
            <Tab eventKey="request_results" title="Request Results" disabled>
            </Tab>
        </Tabs>
    )
}

export default ControlledTabs

