import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { liveChat } from 'meteor/live-chat-meteor-client';

Template.dashboard.events({
	'click .test'(e) {
		e.preventDefault();
		chatbox = document.getElementById('live-chat-box')
		if(chatbox.style.visibility == 'visible')
			chatbox.style.visibility = 'hidden'
		else
			chatbox.style.visibility = 'visible';
	}
});
