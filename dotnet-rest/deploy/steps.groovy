def call(String buildResult) {
  if ( buildResult == "DEPLOY" ) {
    sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
    def lastChanges = readFile('GIT_CHANGES')
    slackSend (channel: "${config.CHANNEL_SLACK}",color: "#FFFF00", message: "Started `${env.JOB_NAME} Build#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges} <${env.RUN_DISPLAY_URL}|Open in Jenkins>")
  }
  if ( buildResult == "SUCCESS" ) {
    slackSend (channel: "${config.CHANNEL_SLACK}",color: "good", message: ":+1::grinning: SUCCESSFUL: Job : `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.RUN_DISPLAY_URL}|Open in Jenkins>")
  }
  else if( buildResult == "FAILURE" ) { 
    slackSend (channel: "${config.CHANNEL_SLACK}",color: 'warning', message: ":-1::face_with_head_bandage: FAILED: Job `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.RUN_DISPLAY_URL}|Open in Jenkins>")
  }
  else if( buildResult == "UNSTABLE" ) { 
    slackSend (channel: "${config.CHANNEL_SLACK}",color: 'warning', message: ":-1::face_with_head_bandage: FAILED: Job `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.RUN_DISPLAY_URL}|Open in Jenkins>")
  }
  else {
    slackSend color: "danger", message: "Job: ${env.JOB_NAME} with buildnumber ${env.BUILD_NUMBER} its resulat was unclear"	
  }
}

def showEnviroment(def config) {
    echo "Enviroment:"
    for(e in config){
        echo "--> ${e}"
    }
}

def login_aws_ecr(def config) {
  withEnv(config) {
    sh 'make login.aws.ecr'
  }
}

def create_repository(def config) {
  withEnv(config) {
    sh 'make create.repository.aws.ecr'
  }
}

def build_lates_image(def config) {
  withEnv(config) {
    sh 'make build'
    sh 'make release'
    sh 'sudo chown -R jenkins:jenkins ${WORKSPACE}'
    sh 'make build.latest'
  }
}

def push_aws_ecr(def config) {
  withEnv(config) {
    sh 'make push.aws.ecr'
  }
}

def register_task_definition_ecr(def config) {
  withEnv(config) {
    sh 'make register.task.definition.ecr'
  }
}

def update_service_ecr(def config) {
  withEnv(config) {
    sh 'make update.service.ecr'
  }
}

def batch_delete_image_aws_ecr(def config) {
  withEnv(config) {
    sh 'make batch.delete.image.aws.ecr'
  }
}

def deregister_task_definitions(def config) {
  withEnv(config) {
    sh 'make deregister.task.definitions'
  }
}

def getRegions(def enviroment) {
  def REGIONS = [
      dev:'eu-west-1',
      pre:'us-west-2',
      prod:'us-east-1'
  ]
  return REGIONS[enviroment]
}

def configs(def enviroment) {
  region = getRegions(enviroment)
  def config = [
    "ENV=${enviroment}",
    "DEPLOY_REGION=${region}",
    "INFRA_BUCKET=infraestructura.${enviroment}",
    "SLACK_CHANNEL=pe-${enviroment}-changelog",
    "ACCOUNT_ID=929226109038",
    "TASK_RAM=256",
    "SRV_NAME=pagoefectivo",
    "MS_NAME=custompayment",
    "BRANCH_BUILD=${enviroment}"
  ]

  return config
}

return this