pipeline {
  agent any
  stages{
    stage('Build'){
      steps{
        echo 'This is build step'
      }
    }
    stage('UnitTest'){
      steps{
        echo "Testing step passed."
      }
    }
    stage('UnitTest2'){
      steps{
        echo "Testing step2 passed."
      }
    }
    stage('UnitTest3'){
      steps{
        echo "Testing step3 passed."
      }
    }
    stage('loop'){
      steps{
        sh '''
            for i in {1..10}; do echo $i; done
        '''
      }
    }
  }
}
