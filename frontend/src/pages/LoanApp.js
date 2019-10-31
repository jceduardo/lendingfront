import React, { useState, useEffect } from 'react'
import LoanForm from '../components/LoanForm'
import FatalError from './FatalError'
import Loading from '../components/Loading'
import url from '../config'

const LoanApp = () => {
  const [form, setForm] = useState({
    bsn_tax_id: '',
    bsn_name: '',
    bsn_address: '',
    bsn_city: '',
    bsn_state: '',
    bsn_postal_code: '',
    bsn_requested_amount: '',
    owr_social_security_number: '',
    owr_name: '',
    owr_email: '',
    owr_address: '',
    owr_city: '',
    owr_state: '',
    owr_postal_code: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [data, setData] = useState({
    loan_decision:'',
    loan_status:''
  })

  const handleChange = e => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async e => {
    setLoading(true)
    e.preventDefault()
    try {
      let config = {
        method: 'POST',
        mode: 'no-cors',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(form)
      }
      let response = await fetch(`${url}`, config).then(res => res.json()).then(data => setData(data))
      setData(response)
      setLoading(false)
    } catch (error) {
      setLoading(false)
      setError(error)
    }
  }

  if (loading)
    return <Loading />

  if (error)
    return <FatalError />

  return <LoanForm
    onChange={handleChange}
    onSubmit={handleSubmit}
    form={form}
    loanDecision={data.loan_decision}
    loanStatus={data.loan_status}
  />
}

export default LoanApp
