
const app = Vue.createApp({
	data() {
		return {
			user: '',
			showParagraph: true,
			bgColor: ''
		};
	},
	computed: {
		input1Classes() {
			return {
				user1: ('user1' == this.user),
				user2: ('user2' == this.user),
				visible: (this.showParagraph),
				hidden: (!this.showParagraph)
			};
		}
	},
	methods: {
		setUser(event) {
			this.user = event.target.value;
		},
		toggleParagraph() {
			this.showParagraph = !this.showParagraph;
		},
		setBgColor(event) {
			this.bgColor = event.target.value;
		}
	}
});

app.mount('#assignment');
