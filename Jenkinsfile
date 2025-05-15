pipeline {
  agent any
  stages{
    stage('Build'){
      steps{
        echo 'This is build step'
        if [ $(java -version 2>&1 | grep version | cut -d '"' -f2 | cut -d '.' -f1) -eq 17 ]; then
          echo "Java version - 17"
        fi
      }
    }
    stage('UnitTest'){
      steps{
        echo "Testing passed."
      }
    }
  }
}
