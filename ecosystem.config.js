module.exports = {
  apps : [{
    name: 'integra',
    cmd: 'src/app.py',
    interpreter: '.env/bin/python3',   
    autorestart: true,
    watch: true,
    pid: '/tmp/integra.pid',
    instances: 1,
    max_memory_restart: '1G',
    env: {
      ENV: 'development',
      PYTHONWARNINGS: 'ignore:Unverified HTTPS request',
      IXC_DOMAIN: 'ixc.test.com.br',
      IXC_KEY: '', //tulio user token
      RC_URL: 'https://chat.test.com.br/',
      RC_USERNAME: 'vbot',
      RC_PASSWORD: 'RC_BOT_PASS',
      PORT: '3000',
      DEBUG: 'True'
    },
    env_production : {
      ENV: 'production',
      PYTHONWARNINGS: 'ignore:Unverified HTTPS request',
      IXC_DOMAIN: 'ixc.test.com.br',
      IXC_KEY: '', //bot user token
      RC_URL: 'https://chat.test.com.br/',
      RC_USERNAME: 'vbot',
      RC_PASSWORD: 'RC_BOT_PASS',
      PORT: '8080',
      DEBUG: 'False'
    }
  }]
};
