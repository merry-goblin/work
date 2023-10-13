const app = Vue.createApp({
	data() {
		return {
			output1: '',
			output2: '',
			storedValue: ''
		};
	},
	methods: {
		showAlert() {
			window.alert("Did you clicked on me? What a clicker you are!");
		},
		aKeyIsDown(event) {
			this.output1 = event.target.value;
		},
		aSecondKeyIsDown(event) {
			this.storedValue = event.target.value;
		},
		enterIsPressed() {
			this.output2 = this.storedValue;
		}
	}
});

app.mount('#assignment');