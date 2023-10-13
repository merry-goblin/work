const app = Vue.createApp({
	data() {
		return {
			number: 0,
		};
	},
	computed: {
		result() {
			let output = '';
			if (this.number < 37) {
				output = "Not there yet";
			}
			else if (this.number === 37) {
				output = this.number;
			}
			else {
				output = "Too much!";
			}
			return output;
		},
	},
	watch: {
		result() {
			let that = this;
			setTimeout(function() {
				if (that.result == 'Too much!') {
					that.number = 0;
				}
			}, 5000);
		},
	},
	methods: {
		add(number) {
			this.number += number;
		},
	}
});

app.mount('#assignment');