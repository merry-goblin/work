const app = Vue.createApp({
	data() {
		return {
			name: "Keller Alexandre",
			age: 38,
			imgLink: 'https://cdn3.bioparc-zoo.fr/wp-content/uploads/2020/02/Bioparc-parc-zoologique-projet-nature-panda-1.jpg',
		};
	},
	methods: {
		getARandomNumber() {
			return Math.random();
		}
	}
});

app.mount('#assignment');