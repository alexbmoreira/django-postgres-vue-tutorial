import api from '@/api/api.service'

async function getDirectors() {
    return api.get(`/directors`)
        .then(response => response.data)
}

export default {
	getDirectors
}