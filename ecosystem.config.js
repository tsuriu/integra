module.exports = {
  apps : [{
    name: 'integraveloo',
    cmd: 'src/app.py',
    interpreter: '.env/bin/python3',   
    autorestart: true,
    watch: true,
    pid: '/tmp/sqdintegra.pid',
    instances: 1,
    max_memory_restart: '1G',
    env: {
      ENV: 'development',
      PYTHONWARNINGS: 'ignore:Unverified HTTPS request',
      IXC_DOMAIN: 'ixc.veloo.com.br',
      IXC_KEY: '165:8e1817e023f5905385b7035208a67c3be5b5a6b08b97dae0dabe33da7bcb21b2', //tulio user token
      RC_URL: 'https://chat.veloo.com.br/',
      RC_USERNAME: 'vbot',
      RC_PASSWORD: 'v3l00@v3l00',
      PORT: '3000',
      DEBUG: 'True'
    },
    env_production : {
      ENV: 'production',
      PYTHONWARNINGS: 'ignore:Unverified HTTPS request',
      IXC_DOMAIN: 'ixc.veloo.com.br',
      IXC_KEY: '178:a4bfdccc42d6a6af79b9ad7b7007ee91b03fb2e8b7433629a89e77a036da2a60', //veloobot user token
      RC_URL: 'https://chat.veloo.com.br/',
      RC_USERNAME: 'vbot',
      RC_PASSWORD: 'v3l00@v3l00',
      PORT: '8080',
      DEBUG: 'False'
    }
  }]
};