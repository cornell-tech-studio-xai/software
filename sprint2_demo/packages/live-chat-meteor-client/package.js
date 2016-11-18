Package.describe({
  name: 'live-chat-meteor-client',
  version: '0.0.1',
  summary: '',
  git: '',
  documentation: 'README.md'
});

Package.onUse(function(api) {
  api.versionsFrom('1.3.2.4');
  api.use('ecmascript');
  api.use('templating');
  api.use('reactive-var');
  api.use('random');
  api.use('ddp');
  api.addFiles('live-chat-meteor-client.css', 'client');
  api.addFiles('live-chat-meteor-client.html', 'client');
  api.addFiles('init.js', ['client', 'server']);
  api.addFiles('live-chat-meteor-client.js', 'client');
  api.export('liveChat');
});

