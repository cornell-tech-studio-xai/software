liveChat = {
    init(clientAppId) {
        let self = this;
        const endpoint = 'http://localhost:3000';
        this.userSessionId = Random.id();
        this.clientAppId = clientAppId;
        this.ddp = DDP.connect(endpoint);
        this.chatCollection = new Mongo.Collection('chat', {connection: this.ddp});
        this.ddp.subscribe('Chat.messagesList', this.clientAppId, this.userSessionId);
        this.messages = this.chatCollection.find({userSessionId: this.userSessionId}, {sort: {date: 1}});
    }
};