import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { liveChat } from 'meteor/live-chat-meteor-client';
import './main.html';
import './loading.html';
import './results.html';
import './dashboard.html';
import './test.html';

Router.route('/', function () {
	this.render('main');
});


Router.route('/Loading');
//Router.route('/Results');
//Router.route('/dashboard');
Router.route('/test');
Meteor.startup(function () {
    // you need to initialize your chatBox here
    // you need to provide your client app id here
    // you need to create a client app in the host app
    liveChat.init('YezcjRwBEAmKSEEjx');
});

Router.map(function () {
   this.route('dashboard', {
        path: '/dashboard/:auth_code',
        data: function () {
                return {"auth_code": this.params.auth_code};
        }

   })
});

function onSignIn(googleUser) {
        // Useful data for your client-side scripts:
        var profile = googleUser.getBasicProfile();
        console.log("ID: " + profile.getId()); // Don't send this directly to your server!
        console.log('Full Name: ' + profile.getName());
        console.log('Given Name: ' + profile.getGivenName());
        console.log('Family Name: ' + profile.getFamilyName());
        console.log("Image URL: " + profile.getImageUrl());
        console.log("Email: " + profile.getEmail());

//         // The ID token you need to pass to your backend:
//         var id_token = googleUser.getAuthResponse().id_token;
//         console.log("ID Token: " + id_token);
};

document.body.style.backgroundImage = "url()";
