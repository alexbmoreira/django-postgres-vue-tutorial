import axios from 'axios'
import Cookies from 'js-cookie'

export default axios.create({
	baseURL: process.env.VUE_APP_URL + '/api',
	timeout: 5000,
	headers: {
		'Content-Type': 'application/json',
		'X-CSRFToken': Cookies.get('csrftoken')
	}
})