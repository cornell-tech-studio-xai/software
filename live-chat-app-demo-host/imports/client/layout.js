import { Template } from 'meteor/templating';
import { ReactiveDict } from 'meteor/reactive-dict';
import { $ } from 'meteor/jquery';
import { Chat, Client } from '../both/collections.js';

// this is just for demo (and article) purposes
// you can check out production ready app here: https://github.com/juliancwirko/s-chat-app

// we can import html templates here
import './layout.html';

// we need a state management we will use reactive-dict (https://atmospherejs.com/meteor/reactive-dict)
// it could be imported from some kind of global state
// here we just use local dictionary
// you can also use ReactiveVar if you want (https://atmospherejs.com/meteor/reactive-var)
const state = new ReactiveDict('');
state.setDefault({
    openedChat: '',
    openedApp: ''
});

// Main template
// We need to subscribe to the data - here client apps and particular chats in the context of the chosen app
Template.main.onRendered(function () {
    const instance = this;
    instance.subscribe('Client.appsList');
    instance.autorun(() => {
        instance.subscribe('Chat.list', state.get('openedApp'));
    });
});
// We configure 'add-new-app' onClick event here
Template.main.events({
    'click .js-add-new-client-app'() {
        const instance = Template.instance();
        const name = instance.$('[name=client-app-name]').val();
        if (name) {
            Meteor.call('addClientApp', name);
            instance.$('[name=client-app-name]').val('');
        }
    }
});
// We prepare data helpers in the main template
Template.main.helpers({
    clientApps() {
        return Client.find();
    },
    clientAppsChatsSessions() {
        var sss = Chat.find({clientAppId: state.get('openedApp')})
            .fetch()
            .map(c => c.userSessionId)
            .filter((v, i, s) => s.indexOf(v) === i);
            state.set('openedChat', sss[sss.length-1])
            // setTimeout(function(){
            //     Meteor.call('process',function(){
            //         state.set('openedChat', sss[sss.length-1])});}, 700);
        return sss;
    },
    chatBoxOpened() {
        return state.get('openedChat');
    }
});

// Client App item template
// We set up chosen appId here
Template.appItem.events({
    'click .js-open-chats'(e) {
        e.preventDefault();
        const data = Template.currentData();
        state.set('openedApp', data.id);
        state.set('openedChat', '');
    }
});

// Chat item template
// We set up opened chatBox by userSessionId
Template.chatItem.events({
    'click .js-open-chat-messages'(e) {
        e.preventDefault();
        const data = Template.currentData();
        state.set('openedChat', data.userSessionId);
    }
});

Template.registerHelper("log", function(something) {
  console.log(something);
});
// Chat box with messages template
// We render chatBox and subscribe to the messeges in the context of a single userSessionId
Template.chatBox.onRendered(function () {
    const instance = Template.instance();
    instance.autorun(() => {
        instance.subscribe('Chat.messagesList', state.get('openedApp'), state.get('openedChat'));
    });
});
// We populate the messages data
Template.chatBox.helpers({
    messages() {
        return Chat.find({clientAppId: state.get('openedApp'), userSessionId: state.get('openedChat')}, {sort: {date: 1}});
    },
    userSessionId() {
        return state.get('openedChat');
    }
});

Template.chatBoxMessageItem.helpers({
    autoRespond: function(msg, sid) {
        var user1 = "Hi";
        var bot1 = "Hi Evan, I’m Amy from x.ai. I am your AI powered personal assistant for scheduling meetings. Want to see how I work? Just ask me any question related to scheduling, such as 'show me how you work' or 'what can you do for me'.";
        user2 = "How do you work?";
        bot2 = "You can interact with me as you would with any other person – and I’ll do all the tedious email ping pong that comes along with scheduling a meeting. All you need to do is cc: amy@x.ai when sending a mail to someone you want to meet";
        user3 = "What do I say?"
        bot3 = "Just say: 'Hi <recipient>, I'm cc'ing my virtual assistant Amy who will find time for us to meet.'";
        user4 = "And what will you do?"
        bot4 = "When you sign up I'll get access to your meeting preferences and calendar. I’ll take into consideration your scheduling hours, office location, conference line, etc when I schedule your meetings.";
        user5 = "How much do you cost?";
        bot5 = "I’m completely FREE! But there is a wait. If you to try me now and get more powerful features, x.ai also offers a paid professional version here: https://x.ai/pricing/";
        user6 = "How do I sign up?";
        bot6 = "Sign up for your free trial here: https://x.ai/";
        user7 = "Will you speak on my behalf?";
        bot7 = "No. I will send the mail as Amy Ingram, but will let the recipient know that I'm an AI powered bot";
        user8 = "What if someone cancels the meeting?"
        bot8 = "I will reschedule with them";
        user_msgs = [user1, user2, user3, user4, user5, user6, user7, user8];
        bot_msgs = [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8];
        for(i=0; i<user_msgs.length; i++){
            if(msg==user_msgs[i] && sid==state.get('openedChat'))
                Meteor.call('addChatMessage', bot_msgs[i], state.get('openedApp'), state.get('openedChat'), false);
        }

    }
});
// We attach onKeydown event to be able to send new messages
Template.chatBox.events({
    'keydown .js-chat-submit-input'(e) {
        const instance = Template.instance();
        const msg = instance.$('.js-chat-submit-input').val();
        const key = e.keyCode || e.which;
        if (key === 13 && !e.shiftKey) {
            e.preventDefault();
            if (msg.trim() !== '') {
                Meteor.call('addChatMessage', msg, state.get('openedApp'), state.get('openedChat'));
                $(e.currentTarget).val('');
            }
        }
    }
})