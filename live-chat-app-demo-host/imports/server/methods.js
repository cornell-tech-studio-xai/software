import { Meteor } from 'meteor/meteor';
import { check } from 'meteor/check';
import {Chat, Client, Banned} from '../both/collections.js';

// IMPORTANT:
// remember that these methods are insecure
// this is just for demo (and article) purposes
// you can check out production ready app here: https://github.com/juliancwirko/s-chat-app

Meteor.methods({
    addClientApp(name) {
        check(name, String);
        Client.insert({name: name});
    },
    addChatMessage(msg, clientAppId, userSessionId, isFromClient) {
        check(msg, String);
        check(clientAppId, String);
        check(userSessionId, String);
        check(isFromClient, Match.Optional(Boolean));
        isFromClient = isFromClient || false;
        Chat.insert({
            msg: msg,
            clientAppId: clientAppId,
            userSessionId: userSessionId,
            date: new Date(),
            isFromClient: isFromClient
        });
    }
});