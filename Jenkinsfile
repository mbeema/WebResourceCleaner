pipeline {
   
    agent { node { label 'TPCATGBUILD01' } }

    parameters {
        string(name: 'TARGET_URL', defaultValue: '', description: 'The URL of the website to crawl.')
        string(name: 'EXCLUDE_URLS', defaultValue: '', description: 'Comma-separated list of URLs to exclude')
    }
    environment {
        DISPLAY = ':0'
    }
   
    stages {

        stage('Setup Environment') {
            steps {
                
                
                // Install Python dependencies
                sh 'pip3 install --user requests selenium beautifulsoup4 Jinja2 webdriver_manager'
            }
        }

       stage('Run Script') {
            steps {
                script {
                    def excludeUrls = params.EXCLUDE_URLS ? params.EXCLUDE_URLS.replaceAll(',', ' ') : ''
                    sh "python3 web_crawler.py --url ${params.TARGET_URL} --exclude ${excludeUrls}"
                }
            }
        }

        stage('Archive Report') {
            steps {
                // Archive the HTML report
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }

        stage('Send Email') {
            steps {
                // Send the HTML report via email
                emailext(
                    subject: "Website Analysis Report for ${params.TARGET_URL}",
                    body: "Please find the attached website analysis report for ${params.TARGET_URL}.",
                    to: 'mbeema@gmail.com',
                    attachmentsPattern: 'report.html'
                )
            }
        }
    }
}

