function installApp() {
    return {
        deferredPrompt: null,
        canInstall: false,
        installing: false,

        init() {
            if (window.matchMedia('(display-mode: standalone)').matches) {
                console.log("App already installed");
                return;
            }

            window.addEventListener('beforeinstallprompt', (e) => {
                e.preventDefault();
                this.deferredPrompt = e;
                this.canInstall = true;
                console.log("Can install app now");
            });

            setTimeout(() => {
                if (!this.canInstall) {
                    console.log("App is not installable – maybe missing manifest, HTTPS, or user engagement?");
                }
            }, 5000);
        },


        async install() {
            if (!this.deferredPrompt) return;
            
            this.installing = true;
            this.deferredPrompt.prompt();
            await this.deferredPrompt.userChoice;
            this.deferredPrompt = null;
            this.canInstall = false;
            this.installing = false;
        }
    }
}