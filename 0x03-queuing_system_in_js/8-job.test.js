describe('createPushNotificationsJobs', () => {
    beforeEach(() => {
      queue.testMode.enter();
    });
  
    afterEach(() => {
      queue.testMode.clear();
    });
  
    it('should throw an error if jobs is not an array', () => {
      expect(() => createPushNotificationsJobs('invalid', queue)).toThrow('Jobs is not an array');
    });
  
    it('should create jobs in the queue', () => {
      const jobs = [
        {
          phoneNumber: '4153518780',
          message: 'This is the code 1234 to verify your account',
        },
        // Add more job objects as needed
      ];
  
      createPushNotificationsJobs(jobs, queue);
  
      expect(queue.testMode.jobs.length).toBe(jobs.length);
  
      const jobIds = jobs.map((job, index) => `job ${index + 1}`);
      expect(queue.testMode.jobs.map(job => job.id)).toEqual(expect.arrayContaining(jobIds));
    });
  });