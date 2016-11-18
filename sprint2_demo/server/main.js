import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {

});

 Meteor.methods({
        parseEmails: function (code) {
            //this.unblock();
            return Meteor.http.call("GET", "http://localhost:5000/parse/" + code);
        }
 });
